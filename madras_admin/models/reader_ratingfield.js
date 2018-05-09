'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_ratingfield', {
    'type': {
      type: DataTypes.STRING,
    },
    'prompt': {
      type: DataTypes.STRING,
    },
    'min_number': {
      type: DataTypes.INTEGER,
    },
    'max_number': {
      type: DataTypes.INTEGER,
    },
    'options': {
      type: DataTypes.STRING,
    },
    'rating_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'reader_ratingfield',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

