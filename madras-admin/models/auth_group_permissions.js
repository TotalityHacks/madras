'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('auth_group_permissions', {
  }, {
    tableName: 'auth_group_permissions',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.auth_group, {
      foreignKey: 'group_id',
      
      as: '_group_id',
    });
    
    Model.belongsTo(models.auth_permission, {
      foreignKey: 'permission_id',
      
      as: '_permission_id',
    });
    
  };

  return Model;
};

