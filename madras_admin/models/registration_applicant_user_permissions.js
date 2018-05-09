'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant_user_permissions', {
    'applicant_id': {
      type: DataTypes.INTEGER,
    },
    'permission_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'registration_applicant_user_permissions',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

